import connectfour.utils as utils
from connectfour.display import ConsoleDisplay
from connectfour.TestEnv import TestEnvironment


def main():
    env = TestEnvironment()
    display = ConsoleDisplay()
    bot = utils.get_agent("random")
    env.init(bot, 5)
    display.render(env.obs, env.config)
    print(display)
    dl_bot = utils.get_agent("agents/deepbot.py")
    val = dl_bot(env.obs, env.config)
    env.obs.step(val, env.config)
    display.render(env.obs, env.config)
    print(display)


if __name__ == "__main__":
    main()
