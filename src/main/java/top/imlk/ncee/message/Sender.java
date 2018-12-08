package top.imlk.ncee.message;

import top.imlk.ncee.abstracts.LogableRunnable;
import top.imlk.ncee.abstracts.StopAbleBlockingQueue;

import java.util.concurrent.TimeUnit;

public interface Sender {

    boolean willBeMoreData();

    default <T> boolean determineSend(StopAbleBlockingQueue<T> stopAbleBlockingQueue, T t, long timeout) throws InterruptedException {

        while (true) {
            boolean succ = stopAbleBlockingQueue.offer(t, timeout, TimeUnit.MILLISECONDS);
            if (!succ) {
                if (!stopAbleBlockingQueue.needMoreData()) {
                    return false;
                }
            } else {
                return true;
            }

            if (this instanceof LogableRunnable) {
                ((LogableRunnable) this).logger.info("{} 重试offer {}", this, t);
            }
        }

    }

}
