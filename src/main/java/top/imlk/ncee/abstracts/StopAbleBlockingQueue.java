package top.imlk.ncee.abstracts;

import top.imlk.ncee.message.Receiver;
import top.imlk.ncee.message.Sender;

import java.util.*;
import java.util.concurrent.ArrayBlockingQueue;

public class StopAbleBlockingQueue<T> extends ArrayBlockingQueue<T> implements Sender, Receiver {
    public StopAbleBlockingQueue(int capacity) {
        super(capacity);
    }

    public StopAbleBlockingQueue(int capacity, boolean fair) {
        super(capacity, fair);
    }

    public StopAbleBlockingQueue(int capacity, boolean fair, Collection<? extends T> c) {
        super(capacity, fair, c);
    }


    public Set<Sender> senders = new LinkedHashSet<>();

    public synchronized void registerSender(Sender sender) {
        senders.add(sender);
    }

    public synchronized void unregisterSender(Sender sender) {
        senders.remove(sender);
    }

    public synchronized int countSender() {

        return senders.size();
    }


    @Override
    public synchronized boolean willBeMoreData() {
        boolean more = false;
        for (Sender sender : senders) {
            if (sender != null && sender.willBeMoreData()) {
                more = true;
            }
        }

        return more;
    }


    public Set<Receiver> receivers = new LinkedHashSet<>();

    public synchronized void registerReceiver(Receiver receiver) {
        receivers.add(receiver);
    }

    public synchronized void unregisterReceiver(Receiver receiver) {
        receivers.remove(receiver);
    }

    public synchronized int countReceiver() {

        return receivers.size();
    }


    @Override
    public boolean needMoreData() {
        boolean more = false;
        for (Receiver receiver : receivers) {
            if (receiver != null && receiver.needMoreData()) {
                more = true;
            }
        }

        return more;
    }
}
