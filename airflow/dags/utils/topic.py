# TODO: Replace with a proper algorithm to figure out the topic later
topics = [
  'trump',
  'canada',
  'usa',
  'russia',
  'syria',
  'murder',
  'criminal',
  'flu',
  'outbreak',
  'covid',
  'idol',
  'singer',
  'grammy',
  'apple',
  'google',
  'tech',
  'layoff',
  'layoffs',
  'mlb',
  'nfl',
  'nba',
  'sports',
  'diddy'
]

def determine_article_topic(title: str = '', description: str = '') -> str:  
  title_lower = ''
  description_lower = ''
  
  # in some cases, title or description can be null
  title_lower = title.lower() if title else ''
  description_lower = description.lower() if description else ''
  
  for topic in topics:
    if topic in title_lower or topic in description_lower:
      return topic

  return 'other'
