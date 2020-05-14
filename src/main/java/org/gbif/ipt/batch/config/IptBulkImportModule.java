package org.gbif.ipt.batch.config;

import com.google.inject.AbstractModule;
import org.gbif.ipt.batch.GBIFIdentifierMap;
import org.gbif.registry.ws.client.guice.RegistryWsClientModule;
import org.gbif.utils.file.properties.PropertiesUtil;
import org.gbif.ws.client.guice.AnonymousAuthModule;

import java.io.IOException;
import java.util.Properties;

public class IptBulkImportModule extends AbstractModule {

  public static final String APPLICATION_PROPERTIES = "application.properties";

  @Override
  protected void configure() {
    try {
      Properties properties = PropertiesUtil.loadProperties(APPLICATION_PROPERTIES);

      // configure GBIF API authentication
      install(new AnonymousAuthModule());

      // bind registry service
      install(new RegistryWsClientModule(properties));
    } catch (IllegalArgumentException e) {
      this.addError(e);
    } catch (IOException e) {
      this.addError(e);
    }
  }
}
