package org.gbif.watchdog.config;

import java.io.IOException;
import java.util.Properties;

import org.gbif.api.service.registry.DatasetService;
import org.gbif.checklistbank.ws.client.guice.ChecklistBankWsClientModule;
import org.gbif.metrics.ws.client.guice.MetricsWsClientModule;
import org.gbif.occurrence.ws.client.OccurrenceWsClientModule;
import org.gbif.registry.ws.client.guice.RegistryWsClientModule;
import org.gbif.utils.file.properties.PropertiesUtil;
import org.gbif.ws.client.guice.AnonymousAuthModule;

import com.google.inject.AbstractModule;
import com.google.inject.Guice;

public class WatchdogModule extends AbstractModule {
  public static final String APPLICATION_PROPERTIES = "application.properties";

  @Override
  protected void configure() {
    try {
      Properties properties = PropertiesUtil.loadProperties(APPLICATION_PROPERTIES);

      // bind registry service
      install(new RegistryWsClientModule(properties));

      // bind occurrence service
      install(new OccurrenceWsClientModule(properties));

      // bind metrics service
      install(new MetricsWsClientModule(properties));

      install(new ChecklistBankWsClientModule(properties, true, true));

      // Anonymous authentication module used, webservice client will be read-only
      install(new AnonymousAuthModule());
    } catch (IllegalArgumentException e) {
      this.addError(e);
    } catch (IOException e) {
      this.addError(e);
    }
  }

}
