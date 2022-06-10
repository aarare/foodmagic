def get_similar_glutenfree(foods):
    import pandas as pd
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity

    gluten = pd.read_csv('gluten_similar.csv', index_col=0)

    if len(gluten[gluten['ingredients_new'].str.contains(foods.lower())]) != 0:  # Eğer ingredientsta yoksa yemek ismine bak
        filtered_df = gluten[gluten['ingredients_new'].str.contains(foods.lower())]
    else:
        filtered_df = gluten[gluten['food_name'].str.lower().str.contains(foods.lower())]

    df_wide = pd.pivot_table(filtered_df, values=["stars"],
                             index=["food_name", "users"],
                             aggfunc=np.mean).unstack()

    df_wide = df_wide.fillna(0)
    try:
        dists = cosine_similarity(df_wide)
        dists = pd.DataFrame(dists, columns=df_wide.index)
        dists.index = dists.columns

        foods_summed = dists.apply(lambda row: np.sum(row), axis=1)
        foods_summed = foods_summed.sort_values(ascending=False)
        ranked_foods = foods_summed.index.tolist()

        # print(ranked_foods)

        df_output = pd.DataFrame(
            columns=['food_name', 'ingredients', 'recipe', 'total_time_new', 'nutrition'])

        for j in ranked_foods:
            for i in gluten["food_name"]:
                if j == i:
                    df_output = pd.concat(
                        [df_output, gluten[gluten["food_name"] == i].loc[:, ['food_name', 'ingredients', 'recipe',
                                                                             'total_time_new', 'nutrition']]])
        # df_review = df_output.drop_duplicates(subset="reviews_new")
        df_output = df_output.drop_duplicates(subset="food_name")
        df_output = df_output.iloc[:3, :]

        return df_output

        # df_review = df_review.groupby(["food_name"])["reviews_new"].apply(list) #her yemeğin yorumlarını bir liste yaptı)

        # print(df_review)

    except ValueError:
        print("Oops, misspelled the word. Please check!")