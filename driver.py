import argparse
from statistics import stats
from data_gen import user_generator, user_restaurant_likes_generator, user_product_likes_generator, user_locations_generator
from knn_recommender.predict import predict

def main():
    parser = argparse.ArgumentParser(description='A driver program for misc foodpool script.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-g', '--generator', action='store_true', help='activate generator (use more options)')
    group.add_argument('-s', '--stats', action="store_true", help="show stats about foodpool system")


    parser.add_argument('-u', '--users', type=int, help="add [N] users to foodpool system [this options is used with -g]")
    parser.add_argument('-uul', '--user-user-likes', type=int , help="[N] [this options is used with -g]")
    parser.add_argument('-url', '--user-restaurant-likes', type=int , help="[N] [this options is used with -g]")
    parser.add_argument('-upl', '--user-product-likes', type=int , help="[N] [this options is used with -g]")
    parser.add_argument('-ul', '--user-locations', type=int , help="[N] [this options is used with -g]")
    parser.add_argument('-pknn', '--predict-knn', type=int , help="[id]")
    parser.add_argument('-n', '--predict-knn-n', type=int , help="[id]")

    args = parser.parse_args()

    if args.stats:
        stats.stats()
    elif args.predict_knn:
        print('predicting nearest match using knn ...')
        if args.predict_knn_n:
            predict(args.predict_knn, n=args.predict_knn_n)
        else:
            predict(args.predict_knn)
    elif args.generator:
        if args.users:
            print('generating users ...')
            user_generator.generate(args.users)

        if args.user_user_likes:
            print('generating user restaurant likes...')
            user_generator.generate()

        if args.user_restaurant_likes:
            print('generating user restaurant likes...')
            user_restaurant_likes_generator.generate(args.user_restaurant_likes)

        if args.user_product_likes:
            print('generating user product likes...')
            user_product_likes_generator.generate(args.user_product_likes)

        if args.user_locations:
            print('generating user product locations in the radius of 10 KM nearby Lahore...')
            user_locations_generator.generator(args.user_locations)


if __name__ == '__main__':
    main()