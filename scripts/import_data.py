from champions.models import Champion

def run():
    # Fetch all questions
    #questions = Champion.objects.all()
    # Delete questions
    #questions.delete()

    # insert champions
    print('adding heimerdinger')
    Champion.objects.add('Heimerdinger')
    print('added heimerdinger')