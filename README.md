# Swit(팀명: 502호 프로젝트)

## 👀 서비스 소개
* 서비스명: Gemini-Pro와 날씨 데이터를 이용한 옷차림 추천 및 의류 리사이클링 서비스 
* 서비스설명:
  - 기상청 Open API에서 기온, 습도, 바람, 강수 확률, 자외선 등의 날씨 데이터를 수집하여 Gemini-Pro에게 전달한 후 사용자에게 적절한 옷차림을 추천하고, 의류 리사이클링 기능을 제공하는 서비스
  - 아침마다 어떤 옷을 입어야 할지 고민하는 학생 또는 직장인, 환경 문제에 관심이 있어 새 옷을 구매하기보다는 중고 의류를 원하는 사람 등을 위한 서비스
  - 의류 판매 및 교환 게시글을 작성할 수 있도록 하여 의류 리사이클링을 돕는 서비스
  - 프로필 기능을 통해 사용자의 정보를 살펴보고 거래를 원하는 경우 채팅으로 소통 가능
  - 회원가입 시 본인인증을 필수로 적용하여 신원이 확인된 사용자들과 안전한 소통 가능

 * 특장점:
  - 기존의 옷차림 추천 서비스가 기온 데이터만 활용하고 있다는 점에 착안하여 기온뿐 아니라 습도, 바람, 강수 확률 등 전반적인 데이터를 고려한 날씨별 옷차림 추천 
  - 회원 간 소통을 통해 기존의 옷을 활용할 수 있도록 도와 서비스 활용도를 향상시키고 심각한 환경 오염을 일으키는 의류폐기물 문제 완화
<br>

## 📅 프로젝트 기간
2024.06.17 ~ 2024.07.31 (6주)
<br>

## ⭐ 주요 기능
* Google의 생성형 AI(Gemini-Pro)를 활용한 날씨별 옷차림 추천 기능
* 일일 날씨 데이터 제공 기능
* cool sms를 활용한 본인인증 기능
* 이용자 간 연결을 가능하게 하기 위한 프로필 기능
* 복수의 이미지 첨부가 가능한 글 작성 기능
* 회원 간 원활한 소통을 위한 채팅 기능
  
<br>

## ⛏ 기술스택
<table>
    <tr>
        <th>구분</th>
        <th>내용</th>
    </tr>
    <tr>
        <td>사용언어</td>
        <td>
           PYTHON, HTML, CSS
        </td>
    </tr>
    <tr>
        <td>라이브러리</td>
        <td>
          cool sms, JSON, SQLAlchemy, GEOLOCATION, WEBSOCKET
        </td>
    </tr>
    <tr>
        <td>개발도구</td>
        <td>
           Gemini-Pro, VSCODE
        </td>
    </tr>
    <tr>
        <td>서버환경</td>
        <td>
            Uvicorn
        </td>
    </tr>
    <tr>
        <td>데이터베이스</td>
        <td>
           MySQL
        </td>
    </tr>
    <tr>
        <td>협업도구</td>
        <td>
          GITHUB
    </tr>
</table>

## ⚙ 시스템 아키텍처(구조) 예시 

## 📌 SW유스케이스
![image](https://github.com/user-attachments/assets/b9c7a639-f984-4f80-a14a-64f1b8c6e904)


## 📌 서비스 흐름도
![image](https://github.com/user-attachments/assets/38c92d44-0480-4d4f-8a96-b05ec17c6192)


## 🖥 화면 구성

### 메인페이지
![image](https://github.com/user-attachments/assets/311a46e0-af2d-4897-86ec-94af873470fc)

### 로그인
![image](https://github.com/user-attachments/assets/06fdb2e7-76c9-4d68-9c04-329f31731769)

### 회원가입
![image](https://github.com/user-attachments/assets/39d986e0-0d03-4d82-a5f9-f743f4331b91)

### Swit
![image](https://github.com/user-attachments/assets/16c0be0b-2ce2-4d45-bc02-3a710d49c183)

### Anabada
![image](https://github.com/user-attachments/assets/afcb4beb-5a31-4f06-b5aa-d15fb58cb978)

### 게시글 상세보기
![image](https://github.com/user-attachments/assets/c52e8b43-f03a-4402-baaa-53e5fb621694)

### 글 작성
![image](https://github.com/user-attachments/assets/5970df22-face-424d-9fd0-a8345fd16917)

### Profile
![image](https://github.com/user-attachments/assets/ed1df73c-1836-43dc-a63f-aebdbd24212a)

### Profile 수정
![image](https://github.com/user-attachments/assets/8bb5b0f3-8478-463c-bf32-2d25c0f7d8a2)

### 채팅
![image](![image](https://github.com/user-attachments/assets/210ef03a-e043-4753-a87b-4e478630f397)

## 👨‍👩‍👦‍👦 팀원 역할
<table>
  <tr>
    <td align="center"><img src="https://img1.daumcdn.net/thumb/R1280x0.fjpg/?fname=http://t1.daumcdn.net/brunch/service/user/cnoC/image/4yPtuRXtR0-jusOMCCXb4MeN6zU.jpg" width="100" height="100"/></td>
    <td align="center"><img src="https://item.kakaocdn.net/do/87c749ed284516d92d1f88dd3e37c9bd8f324a0b9c48f77dbce3a43bd11ce785" width="100" height="100"/></td>
    <td align="center"><img src="https://img1.daumcdn.net/thumb/R1280x0.fjpg/?fname=http://t1.daumcdn.net/brunch/service/user/cnoC/image/DGIamHhKg9IlUvvE8Wt1qsmgkb0" width="100" height="100"/></td>
    <td align="center"><img src="https://pbs.twimg.com/media/EKjES0UU4AEpFRV.jpg" width="100" height="100"/></td>
    
   
  </tr>
  <tr>
    <td align="center"><strong>이여름</strong></td>
    <td align="center"><strong>정여진</strong></td>
    <td align="center"><strong>조민정</strong></td>
    <td align="center"><strong>최슬기</strong></td>
    
  </tr>
  <tr>
    <td align="center"><b>PM / Front-end</b></td>
    <td align="center"><b>Back-end / DB / Front-end</b></td>
    <td align="center"><b>Front-end / DB</b></td>
    <td align="center"><b>AI / DA</b></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/Kayadadu" target='_blank'>github</a></td>
    <td align="center"><a href="https://github.com/kzy282" target='_blank'>github</a></td>
    <td align="center"><a href="https://github.com/mj4226" target='_blank'>github</a></td>
    <td align="center"><a href="https://github.com/summerscape" target='_blank'>github</a></td>
  
  </tr>
</table>

## 🤾‍♂️ 트러블슈팅
  
* 문제1<br>
  - 딥러닝 적용 문제: 전체 프로젝트 기간에 비하여 날씨 데이터를 학습시키는 과정이 복잡하고 기간이 오래걸릴 것이라고 판단되었음<br>
  - 해결방안: 날씨별 옷차림 추천 기능을 생성형 AI인 Gemini-Pro를 활용하여 구현하도록 함으로써 기존의 방식보다 단순화하는 방향으로 변경함
 
* 문제2<br>
  - github 활용 문제: github에 가끔씩 Front-end 코드가 업로드 되지 않는 문제 상황이 발생함<br>
  - 해결 방안: 문제 상황 발생 시 팀원 간 직접 코드를 공유하는 방식으로 해결함

