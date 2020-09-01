package org.gbif.ipt.batch;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class GBIFIdentifierMap {

    private static Logger LOG = LoggerFactory.getLogger(GBIFIdentifierMap.class);

    private static Map<String, String> identifiers = new HashMap<String, String>();

    public static String find(String uuid) {
        return identifiers.get("IPT-"+uuid);
    }

    public static boolean init() {
        try {
            String filePath = "/identifiers.csv";
            File file = new File(filePath);
            if (!file.exists()) {
                LOG.error("No identifiers.csv file found");
                LOG.error("GBIF identifiers not initialized !");
                return false;
            }
            Scanner sc = new Scanner(file);
            sc.useDelimiter(";");
            while (sc.hasNext())
            {
                String row = sc.nextLine();
                String[] cells = row.split(";");
                // IPT UUID / GBIF UUID
                identifiers.put(cells[1], cells[0]);
            }
            sc.close();

            LOG.info("GBIF identifiers initialized: "+identifiers.size()+ " identifiers found");
        }
        catch (FileNotFoundException e) {
            LOG.error(e.getMessage());
            return false;
        }

        return (identifiers.size() > 0);
    }
}
