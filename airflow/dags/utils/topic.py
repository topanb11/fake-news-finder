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
  'sports'
  'diddy'
]

def determine_article_topic(title: str = '', description: str = '') -> str:  
  title_lower = ''
  description_lower = ''
  
  # in some cases, title or description can be null
  if title:
    title_lower = title.lower()
    
  if description:
    description_lower = description.lower()
  
  for topic in topics:
    if topic in title_lower or topic in description_lower:
      return topic

  return 'general'
