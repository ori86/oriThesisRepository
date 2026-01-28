package il.co.codeguru.corewars8086;

import com.google.devtools.common.options.OptionsParser;
import il.co.codeguru.corewars8086.cli.HeadlessCompetitionRunner;
import il.co.codeguru.corewars8086.cli.Options;
import il.co.codeguru.corewars8086.gui.CompetitionWindow;

import java.io.IOException;

public class CoreWarsEngine {
  public static void main(String[] args) throws IOException {
    OptionsParser optionsParser = OptionsParser.newOptionsParser(Options.class);
    optionsParser.parseAndExitUponError(args);
    //String survivors_path = args[0];
    //String output_path = args[1];
    Options options = optionsParser.getOptions(Options.class);
    //options.warriorsDir = survivors_path;
    //options.outputFile = output_path;
  
    if (options != null && options.headless) {  // options should never be null
      System.setProperty("java.awt.headless", "true");
      HeadlessCompetitionRunner r = new HeadlessCompetitionRunner(options);
    } else {
      CompetitionWindow c = new CompetitionWindow(options);
      c.setVisible(true);
      c.pack();
      c.ClickStart();
    }
  }
}
