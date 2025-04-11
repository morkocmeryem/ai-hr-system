from matcher import calculate_similarity

cv = "Python, Django, REST, HTML"
job = "Looking for Django developer with Python skills"

score = calculate_similarity(cv, job)
print(f"Benzerlik Skoru: %{score}")
