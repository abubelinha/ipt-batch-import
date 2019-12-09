package org.gbif.ipt.batch;

import com.google.common.base.Strings;
import com.google.inject.Guice;
import com.google.inject.Injector;
import freemarker.cache.ClassTemplateLoader;
import freemarker.cache.TemplateLoader;
import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;
import org.gbif.api.model.registry.Organization;
import org.gbif.api.service.registry.DatasetService;
import org.gbif.api.service.registry.NodeService;
import org.gbif.api.service.registry.OrganizationService;
import org.gbif.metadata.eml.Agent;
import org.gbif.metadata.eml.Eml;
import org.gbif.metadata.eml.EmlFactory;
import org.gbif.metadata.eml.EmlWriter;
import org.gbif.metadata.eml.GeospatialCoverage;
import org.gbif.utils.file.CompressionUtil;
import org.gbif.ipt.batch.config.IptBulkImportModule;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

/**
 */
public class IptBulkImport {

  private static Logger LOG = LoggerFactory.getLogger(IptBulkImport.class);

  private static final Agent rescuer = new Agent();

  // Change these if it's necessary to use a different template
  private static final String SOURCE_DWCA_DATA = "Occurence.txt";
  private static final String META_TEMPLATE = "/gbifFranceMeta.xml";
  private static final String RESOURCE_TEMPLATE = "gbifFranceResource.ftl";

  // Change these according to the target IPT
  static {
    // This Agent's email address must be a user registered with the IPT.
    // rescuer.setEmail("systems@gbif.org");
    rescuer.setEmail("dev@gbif.fr");
  }
  private static final UUID organizationKey = UUID.fromString("1928bdf0-f5d2-11dc-8c12-b8a03c50a862");

  // You probably don't want to change these, they define the structure of the DwC-A and IPT resource derictory.
  private static final String TARGET_EML = "eml.xml";
  private static final String TARGET_OCCURRENCE = "occurrence.txt";
  private static final String TARGET_META = "meta.xml";
  private static final String IPT_RESOURCE = "/resource.xml";
  private static final String IPT_SOURCES = "sources";
  private static final String VERSIONED_EML = "eml-1.0.xml";
  private static final String VERSIONED_DWCA = "dwca-1.0.zip";

  private static final Configuration FTL = provideFreemarker();

  private final DatasetService datasetService;
  private final OrganizationService organizationService;
  private final NodeService nodeService;

  IptBulkImport(DatasetService datasetService,
                OrganizationService organizationService,
                NodeService nodeService) {
    this.datasetService = datasetService;
    this.organizationService = organizationService;
    this.nodeService = nodeService;

    FTL.setTimeZone(TimeZone.getTimeZone("UTC"));
    FTL.setDateTimeFormat("yyyy-MM-dd HH:mm:ss.000 zzz");
  }

  /**
   */
  private void rescue(Path sourceZip) throws IOException, ParserConfigurationException, SAXException, TemplateException, NoSuchFieldException {

    Organization organization = organizationService.get(organizationKey);

    Path tmpDecompressDir = Files.createTempDirectory("ipt-batch-decompress-");
    CompressionUtil.decompressFile(tmpDecompressDir.toFile(), sourceZip.toFile(), true);
    LOG.info("Unzipped to: {}", tmpDecompressDir);

    // Open EML file
    InputStream emlIs = new FileInputStream(new File(tmpDecompressDir.toFile(), "eml.xml"));
    Eml eml = EmlFactory.build(emlIs);

    // ensure license is set!
    if (eml.parseLicenseUrl() == null) {
      throw new NoSuchFieldException("License must always be set!");
    }

    // Set a geospatial description if necessary.
    for (GeospatialCoverage gc : eml.getGeospatialCoverages()) {
      if (Strings.isNullOrEmpty(gc.getDescription())) {
        gc.setDescription("See map.");
      }
    }

//    if (check if we need to override the contacts in the EML){
//      // publishing organisation
//      Agent publishingOrg = new Agent();
//      publishingOrg.setOrganisation(organization.getTitle());
//
//      // add up-to-date point of contact thereby also fulfilling minimum requirement
//      eml.setContacts(Arrays.asList(rescuer));
//
//      // add up-to-date creator thereby also fulfilling minimum requirement in order of priority high to low
//      eml.setCreators(Arrays.asList(publishingOrg, rescuer));
//
//      // add up-to-date metadata provider thereby also fulfilling minimum requirement
//      eml.setMetadataProviders(Arrays.asList(rescuer));
//    }

    // ensure specimen preservation methods are lowercase, otherwise IPT doesn't recognize method
    ListIterator<String> iterator = eml.getSpecimenPreservationMethods().listIterator();
    while (iterator.hasNext()) {
      iterator.set(iterator.next().toLowerCase());
    }

    // reset version to 1.0
    eml.setEmlVersion(1, 0);

    // GBIF FRANCE set default abstract if needed
    if (eml.getAbstract().isEmpty()) {
      List<String> abstr = new ArrayList<String>();
      abstr.add("Default abstract");
      eml.setAbstract(abstr);
    }

    // make DwC-A folder
    File dwcaFolder = Files.createTempDirectory("ipt-batch-result-dwca-").toFile();

    // write eml.xml file to DwC-A folder
    File updatedEml = new File(dwcaFolder, TARGET_EML);
    EmlWriter.writeEmlFile(updatedEml, eml);

    // retrieve source data file, and copy to DwC-A folder
    File rescuedOccurrence = new File(dwcaFolder, TARGET_OCCURRENCE);
    FileUtils.copyFile(new File(tmpDecompressDir.toFile(), SOURCE_DWCA_DATA), rescuedOccurrence);
    long recordCount = Files.lines(rescuedOccurrence.toPath(), StandardCharsets.UTF_8).count() - 1;

    // retrieve meta.xml file, and copy to DwC-A folder
    File rescuedMeta = new File(dwcaFolder, TARGET_META);
    FileUtils.copyInputStreamToFile(IptBulkImport.class.getResourceAsStream(META_TEMPLATE), rescuedMeta);

    // make IPT resource directory
    File iptResourceDir = sourceZip.resolveSibling("IPT-"+ FilenameUtils.removeExtension(sourceZip.getFileName().toString())).toFile();
    iptResourceDir.mkdir();

    {
      // upload to IPT

      // ensure publishing organisation set (prerequisite being the organisation and user must be added to the IPT before it can be loaded)
      // ensure auto-generation of citation turned on
      File resourceXml = new File(iptResourceDir, IPT_RESOURCE);
      writeIptResourceFile(resourceXml, organization.getKey(), rescuer, rescuedOccurrence.length(), recordCount);

      // make sources folder in IPT resource folder
      File sources = new File(iptResourceDir, IPT_SOURCES);
      sources.mkdir();

      // retrieve source data file, and copy to IPT sources folder
      FileUtils.copyFile(rescuedOccurrence, new File(sources, TARGET_OCCURRENCE));

      // write eml.xml file to IPT resource folder
      File iptEml = new File(iptResourceDir, TARGET_EML);
      EmlWriter.writeEmlFile(iptEml, eml);

      // write eml.xml file version 1.0 to IPT resource folder
      File versionedEml = new File(iptResourceDir, VERSIONED_EML);
      EmlWriter.writeEmlFile(versionedEml, eml);
    }

    // write compressed (.zip) DwC-A file version 1.0 to IPT resource folder
    File versionedDwca = new File(iptResourceDir, VERSIONED_DWCA);
    CompressionUtil.zipDir(dwcaFolder, versionedDwca);

    LOG.info("IPT Resource / rescue folder: " + iptResourceDir.getAbsolutePath());

    FileUtils.deleteDirectory(tmpDecompressDir.toFile());
    FileUtils.deleteDirectory(dwcaFolder);
  }

  public static void main(String... args)
    throws IOException, ParserConfigurationException, SAXException, TemplateException, NoSuchFieldException {
    Injector injector = Guice.createInjector(new IptBulkImportModule());
    IptBulkImport rescuer = new IptBulkImport(injector.getInstance(DatasetService.class),
      injector.getInstance(OrganizationService.class), injector.getInstance(NodeService.class));

    if (args.length < 1) {
      System.err.println("Give dataset keys as argument");
      System.exit(1);
    }

    for (String path : args) {
      rescuer.rescue(Paths.get(path));
    }
  }

  /**
   * Writes an {@link Eml} object to an XML file using a Freemarker {@link Configuration}.
   */
  private void writeIptResourceFile(File f, UUID publishingOrganizationKey, Agent rescuer, long occurrenceFileSize, long totalRecords) throws IOException, TemplateException {
    Map<String, Object> map = new HashMap();
    map.put("publishingOrganizationKey", publishingOrganizationKey);
    map.put("rescuer", rescuer);
    map.put("occurrenceFileSize", occurrenceFileSize);
    map.put("created", new Date());
    map.put("totalRecords", totalRecords);
    writeFile(f, RESOURCE_TEMPLATE, map);
  }

  /**
   * Writes a map of data to a UTF-8 encoded file using a Freemarker {@link Configuration}.
   */
  private void writeFile(File f, String template, Object data) throws IOException, TemplateException {
    String result = processTemplateIntoString(FTL.getTemplate(template), data);
    Writer out = org.gbif.utils.file.FileUtils.startNewUtf8File(f);
    out.write(result);
    out.close();
  }

  private String processTemplateIntoString(Template template, Object model) throws IOException, TemplateException {
    StringWriter result = new StringWriter();
    template.process(model, result);
    return result.toString();
  }

  /**
   * Provides a freemarker template loader. It is configured to access the UTF-8 IPT folder on the classpath.
   */
  private static Configuration provideFreemarker() {
    TemplateLoader tl = new ClassTemplateLoader(IptBulkImport.class, "/ipt");
    Configuration fm = new Configuration();
    fm.setDefaultEncoding("utf8");
    fm.setTemplateLoader(tl);
    return fm;
  }
}
