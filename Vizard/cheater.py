from source.util import unserialize, serialize


if __name__ == "__main__":
    ts = '1565205312727'

    d = unserialize('resource/tasks/48b49d70/result_cached_copy.dat')

    df = d.df

    df[df.index > 1567523744282] = [15000, 500, False, 0, 10000, 0, 0, 2523, 0, 2477]

    serialize(d, 'resource/tasks/48b49d70/result_cached.dat')
