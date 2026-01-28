package il.co.codeguru.corewars8086.war;

import il.co.codeguru.corewars8086.cli.Options;
import il.co.codeguru.corewars8086.gui.WarFrame;
import il.co.codeguru.corewars8086.memory.MemoryEventListener;
import il.co.codeguru.corewars8086.utils.EventMulticaster;
import org.apache.commons.math3.util.Precision;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;


public class Competition {

    /** Maximum number of rounds in a single war. */
    public final static int MAX_ROUND = 200000;
    private static final String SCORE_FILENAME= "scores.csv";

    private CompetitionIterator competitionIterator;

    private EventMulticaster competitionEventCaster, memoryEventCaster;
    private CompetitionEventListener competitionEventListener;
    private MemoryEventListener memoryEventListener;

    private final WarriorRepository warriorRepository;
    
    private ExecutorService executorService;

    private War currentWar;

    private int warsPerCombination= 20;

    private int speed;
    public static final int MAXIMUM_SPEED = -1;
    private static final long DELAY_UNIT = 200;
    
    private long seed = 0;

    private boolean abort;
    
    private final Options options;

    public Competition(Options options) throws IOException {
        this(true, options);
    }

    public Competition(boolean shouldReadWarriorsFile, Options options) throws IOException {
        warriorRepository = new WarriorRepository(shouldReadWarriorsFile, options);

        competitionEventCaster = new EventMulticaster(CompetitionEventListener.class);
        competitionEventListener = (CompetitionEventListener) competitionEventCaster.getProxy();
        memoryEventCaster = new EventMulticaster(MemoryEventListener.class);
        memoryEventListener = (MemoryEventListener) memoryEventCaster.getProxy();
        speed = MAXIMUM_SPEED;
        abort = false;
        
        this.options = options;
    }
    public void runCompetition(int warsPerCombination, int warriorsPerGroup, boolean startPaused) throws Exception {
        this.warsPerCombination = warsPerCombination;
        competitionIterator = new CompetitionIterator(
                warriorRepository.getNumberOfGroups(), warriorsPerGroup);

        // run on every possible combination of warrior groups
        competitionEventListener.onCompetitionStart();
        int runWarCount = 0;
        List<WarriorGroup> groups = warriorRepository.getWarriorGroups();
        String[] names = warriorRepository.getGroupNames();

        // find our GA survivor group - any name that contains "try"
        int myIndex = -1;
        for (int i = 0; i < names.length; i++) {
            if (names[i].contains("try")) {
                myIndex = i;
                break;
            }
        }

        if (myIndex == -1) {
            throw new IllegalStateException("No group whose name contains 'try' found");
        }

        for (int warCount = 0; warCount < warriorRepository.getNumberOfGroups(); warCount++) {
            // skip other GA survivors
            if (groups.get(warCount).getName().contains("try")) {
                continue;
            }

            WarriorGroup[] game_groups = new WarriorGroup[2];
            game_groups[0] = groups.get(myIndex);
            game_groups[1] = groups.get(warCount);

            for (int run_index = 0; run_index < options.battlesPerCombo; run_index++) {
                runWarCount++;
                runWar(game_groups, startPaused);
            }

            seed++;
            if (abort) {
                break;
            }
        }

        competitionEventListener.onCompetitionEnd();
        warriorRepository.saveScoresToFile(options.outputFile, runWarCount);
    }

    public void runCompetitionInParallel(int warsPerCombination, int warriorsPerGroup, int threads) throws InterruptedException {
      this.warsPerCombination = warsPerCombination;
      competitionIterator = new CompetitionIterator(warriorRepository.getNumberOfGroups(), warriorsPerGroup);
      competitionEventListener.onCompetitionStart();
  
      executorService = Executors.newFixedThreadPool(threads);

      int runWarCount = 0;
      for (int warCount = 0; warCount < getTotalNumberOfWars(); warCount++) {
        WarriorGroup[] groups;
        groups = warriorRepository.createGroupList(competitionIterator.next());
        if (null == groups) // skip wars without my survivor
            continue;
        runWarCount++;
        int id = warCount;
        long warSeed = seed++;
          WarriorGroup[] finalGroups = groups;
          executorService.submit(() -> {
          try {
            runWarInParallel(finalGroups, warSeed, id);
          } catch (Exception e) {
            throw new RuntimeException(e);
          }
        });
      }
  
      executorService.shutdown();
      boolean finished = executorService.awaitTermination(1, TimeUnit.HOURS);
  
      if (!finished) {
        System.err.println("Note: Competition has timed out after 1h - results may be incorrect.");
      }
      
      executorService = null;
  
      competitionEventListener.onCompetitionEnd();
      warriorRepository.saveScoresToFile(options.outputFile, runWarCount);
    }

    public int getTotalNumberOfWars() {
        return (int) competitionIterator.getNumberOfItems() * warsPerCombination;
    }

    public void runWar(WarriorGroup[] warriorGroups,boolean startPaused) throws Exception {
        currentWar = new War(memoryEventListener, competitionEventListener, startPaused, options);
        currentWar.setSeed(this.seed);
        competitionEventListener.onWarStart(seed);
        currentWar.loadWarriorGroups(warriorGroups);
        // create array of staying alive time
        String names;
        String[] warriors;
        final HashMap<String, Float> alive_time = new HashMap<>();

        // go go go!
        int round = 0;
        while (round < MAX_ROUND) {
            competitionEventListener.onRound(round);
            names = currentWar.getRemainingWarriorNames();
            names = names.replace(" ", ""); //avoid spaces
            warriors = names.split(",");
            for (String warrior : warriors) {
                alive_time.put(warrior, (float) round);
            }
            competitionEventListener.onEndRound();

            // apply speed limits
            if (speed != MAXIMUM_SPEED) {
                // note: if speed is 1 (meaning game is paused), this will
                // always happen
                if (round % speed == 0) {
                    Thread.sleep(DELAY_UNIT);
                }

                if (speed == 1) { // paused
                    continue;
                }
            }

            //pause
            while (currentWar.isPaused()) Thread.sleep(DELAY_UNIT);

            //Single step run - stop next time
            if (currentWar.isSingleRound())
                currentWar.pause();

            if (currentWar.isOver()) {
                break;
            }

            currentWar.nextRound(round);

            ++round;
        }
        competitionEventListener.onRound(round);

        int numAlive = currentWar.getNumRemainingWarriors();
        names = currentWar.getRemainingWarriorNames();

        if (numAlive == 1) { // we have a single winner!
            competitionEventListener.onWarEnd(CompetitionEventListener.SINGLE_WINNER, names);
        } else if (round == MAX_ROUND) { // maximum round reached
            competitionEventListener.onWarEnd(CompetitionEventListener.MAX_ROUND_REACHED, names);
        } else { // user abort
            competitionEventListener.onWarEnd(CompetitionEventListener.ABORTED, names);
        }

        int finalRound = round; // we're here after the war termination
        //alive_time.forEach((k , v) -> alive_time.put(k, Precision.round(v/ finalRound, 3)));
        currentWar.updateScores(warriorRepository, alive_time, finalRound);
        //currentWar.updateAliveTime(warriorRepository, alive_time);
        currentWar = null;
    }
  
  public void runWarInParallel(WarriorGroup[] warriorGroups, long seed, int id) throws Exception {
    War war = new War(memoryEventListener, competitionEventListener, false, options);
    war.setSeed(seed);
    boolean selectedAsCurrent = false;
    
    // Set current war as a
    synchronized (this) {
      if (this.currentWar == null) {
        this.currentWar = war;
        selectedAsCurrent = true;
      }
    }
  
    competitionEventListener.onWarStart(seed);
    war.loadWarriorGroups(warriorGroups);
    String names;
    String[] warriors;
    final HashMap<String, Float> alive_time = new HashMap<>();
    
    int round = 0;
    while (round < MAX_ROUND) {
      competitionEventListener.onRound(round);
      names = currentWar.getRemainingWarriorNames();
      names = names.replace(" ", ""); //avoid spaces
      warriors = names.split(",");
      for (String warrior : warriors) {
          alive_time.put(warrior, (float) round);
      }
      competitionEventListener.onEndRound();
      
     if (selectedAsCurrent && speed != MAXIMUM_SPEED) {
       if (round % speed == 0) {
         Thread.sleep(DELAY_UNIT);
       }
     }
      
      if (war.isOver()) {
        break;
      }
      
      war.nextRound(round);
      ++round;
    }
    
    competitionEventListener.onRound(round);
    
    int numAlive = war.getNumRemainingWarriors();
    names = war.getRemainingWarriorNames();
    
    if (numAlive == 1) { // we have a single winner!
      competitionEventListener.onWarEnd(CompetitionEventListener.SINGLE_WINNER, names);
    } else if (round == MAX_ROUND) { // maximum round reached
      competitionEventListener.onWarEnd(CompetitionEventListener.MAX_ROUND_REACHED, names);
    } else { // user abort
      competitionEventListener.onWarEnd(CompetitionEventListener.ABORTED, names);
    }

    if (selectedAsCurrent) {
      synchronized (this) {
        this.currentWar = null;
      }
    }
    
    synchronized (warriorRepository) {
      int finalRound = round; // we're here after the war termination
      alive_time.forEach((k , v) -> alive_time.put(k, Precision.round(v/ finalRound, 3)));
      war.updateScores(warriorRepository, alive_time, finalRound);
      //war.updateAliveTime(warriorRepository, alive_time);
    }
  }
  
  public int getCurrentWarrior() {
        if (currentWar != null) {
            return currentWar.getCurrentWarrior();
        } else {
            return -1;
        }
    }

    public void addCompetitionEventListener(CompetitionEventListener lis) {
        competitionEventCaster.add(lis);
    }
        public void removeCompetitionEventListener(CompetitionEventListener lis) {
    	competitionEventCaster.remove(lis);
    }
    
    public void addMemoryEventLister(MemoryEventListener lis) {
        memoryEventCaster.add(lis);
    }

    public void removeMemoryEventLister(MemoryEventListener lis) {
    	memoryEventCaster.remove(lis);
    }
    
    public WarriorRepository getWarriorRepository() {
        return warriorRepository;
    }

    /**
     * Set the speed of the competition, wither MAX_SPEED or a positive integer 
     * when 1 is the slowest speed
     * @param speed
     */
    public void setSpeed(int speed) {
        this.speed = speed;
    }

    public int getSpeed() {
        return speed;
    }

    public void setAbort(boolean abort) {
        this.abort = abort;
        
        if (abort && executorService != null) {
            executorService.shutdownNow();
            executorService = null;
        }
    }
    
    
    public War getCurrentWar(){
    	return currentWar;
    }
    
    public void setSeed(long seed){
    	this.seed = seed;
    }

    public long getSeed(){
        return seed;
    }
    
}