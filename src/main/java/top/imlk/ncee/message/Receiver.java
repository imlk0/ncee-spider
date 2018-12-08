package top.imlk.ncee.message;

import top.imlk.ncee.abstracts.LogableRunnable;
import top.imlk.ncee.abstracts.StopAbleBlockingQueue;

import java.util.concurrent.TimeUnit;

public interface Receiver {
    boolean needMoreData();

    default <T> T determineReceive(StopAbleBlockingQueue<T> stopAbleBlockingQueue, long timeout) throws InterruptedException {

        while (true) {
            T t = stopAbleBlockingQueue.poll(timeout, TimeUnit.MILLISECONDS);
            if (t == null) {
                if (!stopAbleBlockingQueue.willBeMoreData()) {
                    return null;
                }
            } else {
                return t;
            }

            if (this instanceof LogableRunnable) {
                ((LogableRunnable) this).logger.info("{} 重试poll", this);
            }
        }
    }

}
