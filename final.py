class Restaurant:

    def __init__(self, max_Price, people, min_Price, cuisine, locality, favr=""):
        self.max_Price = max_Price
        self.people = people
        self.min_Price = min_Price
        self.cuisine = cuisine
        self.locality = locality
        self.favr = favr

    @classmethod
    def rest(cls, self):

        import pandas as pd
        import sqlite3

        cnx = sqlite3.connect('roop.db')
        lko_rest = pd.read_sql_query("SELECT * FROM rest", cnx)
        cnx.close()
        lko_rest = lko_rest.drop_duplicates(subset='address', keep='first')

        def fav(lko_rest1):

            lko_rest1 = lko_rest1.reset_index()

            from sklearn.feature_extraction.text import CountVectorizer

            count1 = CountVectorizer(stop_words='english')
            count_matrix = count1.fit_transform(lko_rest1['highlights'])

            from sklearn.metrics.pairwise import cosine_similarity

            cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

            sim = list(enumerate(cosine_sim2[0]))
            sim = sorted(sim, key=lambda x: x[1], reverse=True)
            sim = sim[1:11]
            indi = [i[0] for i in sim]

            final = lko_rest1.copy().iloc[indi[0]]
            final = pd.DataFrame(final)
            final = final.T

            for i in range(1, len(indi)):

                final1 = lko_rest1.copy().iloc[indi[i]]
                final1 = pd.DataFrame(final1)
                final1 = final1.T
                final = pd.concat([final, final1])

            return final

        def rest_rec(cost, people=2, min_cost=0, cuisine=[], Locality=[], fav_rest="", lko_rest=lko_rest):

            cost = cost+100+100

            x = cost/people
            y = min_cost/people

            lko_rest1 = lko_rest.copy().loc[lko_rest['locality'] == Locality[0]]

            for i in range(1, len(Locality)):

                lko_rest2 = lko_rest.copy().loc[lko_rest['locality'] == Locality[i]]
                lko_rest1 = pd.concat([lko_rest1, lko_rest2])
                lko_rest1.drop_duplicates(
                    subset='name', keep='last', inplace=True)

            lko_rest_locale = lko_rest1.copy()

            lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] <= x]
            lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] >= y]

            lko_rest_locale['Start'] = lko_rest_locale['cuisines'].str.find(cuisine[0])
            lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]

            for i in range(1, len(cuisine)):

                lko_rest_locale['Start'] = lko_rest_locale['cuisines'].str.find(
                    cuisine[i])
                lko_rest_cu = lko_rest_locale.copy(
                ).loc[lko_rest_locale['Start'] >= 0]
                lko_rest_cui = pd.concat([lko_rest_cui, lko_rest_cu])
                lko_rest_cui.drop_duplicates(
                    subset='name', keep='last', inplace=True)

            if fav_rest != "":

                favr = lko_rest.loc[lko_rest['name']
                                    == fav_rest].drop_duplicates()
                favr = pd.DataFrame(favr)
                lko_rest3 = pd.concat([favr, lko_rest_cui])
                lko_rest3.drop('Start', axis=1, inplace=True)
                rest_selected = fav(lko_rest3)
            else:
                lko_rest_cui = lko_rest_cui.sort_values(
                    'score', ascending=False)
                rest_selected = lko_rest_cui.head(10)

            return(rest_selected)

        rest_sugg = rest_rec(self.max_Price, self.people,
                             self.min_Price, self.cuisine, self.locality, self.favr)

        rest_list1 = rest_sugg.copy().loc[:, [
            'name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines']]

        rest_list = pd.DataFrame(rest_list1)
        rest_list = rest_list.reset_index()
        rest_list = rest_list.rename(columns={'index': 'res_id'})
        rest_list.drop('res_id', axis=1, inplace=True)
        rest_list = rest_list.T
        self.rest_list = rest_list
        # rest_list.to_json(r'C:\Users\Dell\Desktop\mnee\rest_list1.json')
        # return(rest_list)
# ansh = Restaurant()
# Restaurant.rest(ansh)
# ans=ansh.rest_list
