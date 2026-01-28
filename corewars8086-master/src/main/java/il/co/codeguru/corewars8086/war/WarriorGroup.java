package il.co.codeguru.corewars8086.war;

import java.util.ArrayList;
import java.util.List;

public class WarriorGroup {
    private String name;
    private ArrayList<WarriorData> warriorData;
    private List<Float> scores;
    private float groupScore;
    private float groupBytes;
    private List<Float> aliveTime;
    private List<Float> bytesWritten;

    public WarriorGroup(String name) {
        this.name = name;
        warriorData = new ArrayList<>();
        scores = new ArrayList<>();
        aliveTime = new ArrayList<>();
        bytesWritten = new ArrayList<>();
    }

    public void addWarrior(WarriorData data) {
        warriorData.add(data);
        scores.add(0f);
        aliveTime.add(0f);
        bytesWritten.add(0f);
    }

    public List<WarriorData> getWarriors() {
        return warriorData;
    }

    public List<Float> getScores() {
        return scores;
    }

    public String getName() {
        return name;
    }

    public float getGroupScore() {
        return groupScore;
    }

    public float getGroupBytes() {
        return groupBytes;
    }

    public List<Float> getAliveTime() { return aliveTime; }

    public List<Float> getBytesWritten() { return bytesWritten; }

    public int addScoreToWarrior(String name, float score, float alive, float bytes) {
        // find this warrior
        int i;
        for (i = 0; i < warriorData.size(); i++) {
            if (warriorData.get(i).getName().equals(name)) {
                scores.set(i, scores.get(i) + score);
                aliveTime.set(i, aliveTime.get(i) + alive);
                bytesWritten.set(i, bytesWritten.get(i) + bytes);
                break;
            }
        }
        groupScore += score;
        groupBytes += bytes;

        return i;
    }

    public int addAliveTimeToWarrior(String name, float value) {
        // find this warrior
        int i;
        for (i = 0; i < warriorData.size(); i++) {
            if (warriorData.get(i).getName().equals(name)) {
                aliveTime.set(i, aliveTime.get(i) + value);
                break;
            }
        }
        //groupScore += value;
        return i;
    }

    public int addBytesWrittenToWarrior(String name, int value) {
        // find this warrior
        int i;
        for (i = 0; i < warriorData.size(); i++) {
            if (warriorData.get(i).getName().equals(name)) {
                bytesWritten.set(i, bytesWritten.get(i) + value);
                break;
            }
        }
        return i;
    }
}