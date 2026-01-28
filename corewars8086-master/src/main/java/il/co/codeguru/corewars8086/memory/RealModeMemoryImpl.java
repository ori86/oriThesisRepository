package il.co.codeguru.corewars8086.memory;

/**
 * Implements the RealModeMemory interface using a buffer.
 *
 * @author DL
 */
public class RealModeMemoryImpl extends AbstractRealModeMemory {

    /** Listener to memory events */
    private MemoryEventListener listener;

    /** Actual memory data */
    private byte[] m_data;

    /**
     * Constructor.
     */
    public RealModeMemoryImpl() {
        m_data = new byte[RealModeAddress.MEMORY_SIZE];
    }

    /**
     * Reads a single byte from the specified address.
     *
     * @param address    Real-mode address to read from.
     * @return the read byte.
     * 
     * @throws MemoryException  on any error. 
     */
    public byte readByte(RealModeAddress address) {
        return m_data[address.getLinearAddress()];		
    }

    /**
     * Writes a single byte to the specified address.
     *
     * @param address Real-mode address to write to.
     * @param value   Data to write.
     * @return
     * @throws MemoryException on any error.
     */
    public int writeByte(RealModeAddress address, byte value) {
        m_data[address.getLinearAddress()] = value;
        if (listener != null) {
            boolean is_new_write = listener.onMemoryWrite(address);
            if (is_new_write) {
                // Write to new place in memory was performed by the warrior
                return 1;
            }
        }
        // The warrior wrote to a place it already was the last to write in
        return 0;
    }

    /**
     * Reads a single byte from the specified address, in order to execute it.
     *
     * @param address    Real-mode address to read from.
     * @return the read byte.
     * 
     * @throws MemoryException  on any error. 
     */
    public byte readExecuteByte(RealModeAddress address) {
        return m_data[address.getLinearAddress()];		
    }	

    /**
     * @return Returns the listener.
     */
    public MemoryEventListener getListener() {
        return listener;
    }
    /**
     * @param listener The listener to set.
     */
    public void setListener(MemoryEventListener listener) {
        this.listener = listener;
    }
}
