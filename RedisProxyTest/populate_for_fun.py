"""
These request tests are to be run against a RedisProxy configured
with a cache that has a max key value pair count of 3 and whose key value pairs
expire after 2 seconds.
"""
from my_test_engine import MyTestEngine


def main():
    engine = MyTestEngine()
    engine.populate_redis({'SEGMENT': 'hire me :)'})
    print("****************************************************************\n"
          "***                                                          ***\n"
          "**                       Tests completed.                     **\n"
          "*                                                              *\n"
          "*                           Try it out                         *\n"
          "*           http://127.0.0.1:5000?requestedKey=SEGMENT         *\n"
          "*                                                              *\n"
          "*                                                              *\n"
          "**              Press ctrl+C to end this session.             **\n"
          "***                                                          ***\n"
          "****************************************************************\n")


if __name__ == '__main__':
    main()
