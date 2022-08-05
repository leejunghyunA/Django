from django.db import models

# CharField = 문자를 담는 필드/ TextFied = 문자열의 길이 제한이 없음/ DateTimeField = 월,일,시,분,초를 기록할 수 있게 해주는 필드
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    # <자동으로 작성시간과 수정시간 저장>
    # created_at = 처음으로 레코드가 생성될 때 현재 시각으로 자동저장
    # updated_at = 수정해 다시 저장 할 때마다 그 시각이 저장되도록 해줌 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    # 관리자 페이지에서 Post 목록에 title제목과 번호 출력되도록 해줌 self.pk-해당포스트의 pk 값, self.title-해당 포스트의 title값
    # pk는 장고의 모델에 기본적으로 생성되는 필드 = 각 레코드의 고유값 (like 인덱스 번호와 비슷)
    def __str__(self):
        return f'[{self.pk}]{self.title}'