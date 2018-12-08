package top.imlk.ncee.abstracts;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public abstract class LogableRunnable implements Runnable {
    public Logger logger = LoggerFactory.getLogger(this.getClass());

    @Override
    public void run() {
        logger.info("{} 运行", this);
        doRun();
        logger.info("{} 退出", this);

    }

    protected abstract void doRun();
}
