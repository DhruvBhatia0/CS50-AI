import pagerank
a = {'page1':('page2','page3'),'page2':('page3',),'page3':('page2','page1')}
print(a)
print(type(a))
print(pagerank.transition_model(a, 'page3', 0.85))
