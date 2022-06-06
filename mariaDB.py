import pymysql

# 회원정보 조회
def informationSelect():
    # # DB 연동
    # conn = MongoClient('mongodb://localhost:27017/')  # MongoDB IP : 127.0.0.1, PORT : 27017, use information
    # # DB 생성
    # informationDB = conn['information']
    # global idChkDictionary
    # x = informationDB.information.count_documents( {"id":id} )

    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select * from information;")
            rs = curs.fetchall()
            print(rs)
            informationList = []
            for row in rs:
                informationList.append(row)
            return informationList
    finally:
        conn.close()


# id 존재 개수 조회
def idChk(id):
    # # DB 연동
    # conn = MongoClient('mongodb://localhost:27017/')  # MongoDB IP : 127.0.0.1, PORT : 27017, use information
    # # DB 생성
    # informationDB = conn['information']
    # global idChkDictionary
    # x = informationDB.information.count_documents( {"id":id} )

    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select * from information where id = '" + id + "';")
            x = curs.rowcount  # 조회된 값 개수
    finally:
        conn.close()  # DB 종료

    return x

# print(idChk("kimsubin"))
# print(idChk(""))


# 제품 정보 조회
def productSelect():
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select * from product;")
            rs = curs.fetchall()
            # print(rs)
            productList = []
            for row in rs:
                productList.append(row)
            return productList
    finally:
        conn.close()


# 유통기한 정보 조회
def expirydateSelect(code):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select expirydate from expirydate where code='" + code + "';")
            rs = curs.fetchall()
            # print(rs)
            expirydateList = []
            for row in rs:
                expirydateList.append(row)
            return expirydateList
    finally:
        conn.close()


# 제품 정보와 유통기한 정보 조인 조회
def productexpirydateSelect():
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select p.name, p.id, p.code, p.quantity, p.price, p.registerdate, p.period, e.expirydate from product as p inner join expirydate as e	on p.code = e.code;")
            rs = curs.fetchall()
            # print(rs)
            productexpirydateList = []
            for row in rs:
                productexpirydateList.append(row)
            return productexpirydateList
    finally:
        conn.close()


# 해당 제품의 수량 조회
def quantitySelect(name, code):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select quantity from product where name='" + name + "' and code='" + code + "';")
            rs = curs.fetchall()
            # print(rs)
            quantitydateList = []
            for row in rs:
                quantitydateList.append(row)
            return quantitydateList[0][0]
    finally:
        conn.close()

# print(quantitySelect("sandwich", "sandwich220603062001"))


# 권한 부여
def powerUpdate(power, id):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("update information set power = '" + power + "' where id = '" + id + "';")
        conn.commit()
    finally:
        conn.close()  # DB 종료


# 판매된 제품 수량 업데이트
def quantityUpdate(quantityBefore, quantityBuy, code):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("update product set quantity = '" + str(int(quantityBefore)-int(quantityBuy)) + "' where code = '" + code + "';")
        conn.commit()
    finally:
        conn.close()  # DB 종료


# 접속 속도 우선순위 : 1) 고객 2) 직원 3) 관리자
def login(id, pw):  # 로그인
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select * from information where power = 'customer' and id = '" + id + "' and pw='" + pw + "';")
            resultCustomer = curs.rowcount  # 조회된 값 개수
            curs.execute("select * from information where power = 'staff' and id = '" + id + "' and pw='" + pw + "';")
            resultStaff = curs.rowcount  # 조회된 값 개수
            curs.execute("select * from information where power = 'manager' and id = '" + id + "' and pw='" + pw + "';")
            resultManager = curs.rowcount  # 조회된 값 개수

        if resultCustomer == 1:
            return "resultCustomer"
        elif resultStaff == 1:
            return "resultStaff"
        elif resultManager == 1:
            return "resultManager"
        else:
            return "resultNone"
        print("resultCustomer :", resultCustomer, "resultStaff :", resultStaff, "resultManager :", resultManager)
    except Exception as e:
        print("Error :", e)
        return e
    finally:
        conn.close()  # DB 종료

# login("kimsubin", "kimsubin")


def genderSelect(id, pw):  # 성별 조회
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select gender from information where id='" + id + "' and pw='" + pw + "';")
            rs = curs.fetchall()
            # print(rs)
            genderList = []
            for row in rs:
                genderList.append(row)
            return genderList[0][0]
    finally:
        conn.close()  # DB 종료


# 회원가입
def signUpInsert(name, id, pw, phone, gender, age):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("insert into information values ('customer', '" + name + "', '" + id + "', '" + pw + "', '" + phone
                         + "', '" + gender  + "', '" + age + "');")  # 기본 권한 customer
        conn.commit()
    finally:
        conn.close()


# 제품 등록
def productInsert(name, id, code, quantity, price, period):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            # 제품명, 제품 ID, 제품 시리얼 코드, 수량, 가격, 등록일자 : now(), 유통기간
            curs.execute("insert into product values ('" + name + "', '" + id + "', '" + code + "', '" + quantity + "', '" + price + "', now(), '" + period + "' );")
            # TypeError: can only concatenate str (not "int") to str 문자열로 삽입
        conn.commit()
    finally:
        conn.close()

# productInsert('name', 'id', 'code', '22', '1500', '88')


# 유통기한 등록
def expirydateInsert(code):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            # 제품 시리얼 코드로 해당하는 유통기간만큼을 더한 유통기한을 구해 등록
            curs.execute("insert into expirydate values ('" + code + "', ( select date_add( (select registerdate from product where code = '" + code + "'), interval (select period from product where code = '" + code + "') day) ) );""")
        conn.commit()
    finally:
        conn.close()

# expirydateInsert("code")


# <1> 매출 등록
def productSaleInsert(type, name, quantity, price):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            # type : 직원 주문일 경우 staff. 고객 주문일 경우 customer.
            curs.execute("insert into productSale values ('" + type + "', now(), '" + name + "', '" + quantity + "', '" + price + "', 'None');")
        conn.commit()
    finally:
        conn.close()


# <2> 판매된 제품 유통기한 정보 삭제
def expirydateDelete(code):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("delete from expirydate where code='" + code + "';")
        conn.commit()
    finally:
        conn.close()


# <3> 판매된 제품 정보 삭제
def productSaleDelete(name, code, quantity):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("delete from product where name='" + name + "' and code='" + code + "' and quantity='" + quantity + "';")
        conn.commit()
    finally:
        conn.close()




# 순위 검색
def rankSelect():
    global rank  # 전역변수 리스트 사용
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            # 문자열 타입 숫자의 내림차순
            curs.execute("select * from score order by score * 1 desc limit 3;")
            cnt = curs.rowcount  # 검색한 row 개수를 변수에 저장
            rs = curs.fetchall()

            if cnt == 0:
                rank.clear()
                rank.append("1등 공석")  # 1등 이름
                rank.append("0")  # 1등 점수
                rank.append("2등 공석")  # 2등 이름
                rank.append("0")  # 2등 점수
                rank.append("3등 공석")  # 3등 이름
                rank.append("0")  # 3등 점수
                print(rank)
            elif cnt == 1:
                rank.clear()
                rank.append(rs[0][0])  # 1등 이름
                rank.append(rs[0][1])  # 1등 점수
                rank.append("2등 공석")  # 2등 이름
                rank.append("0")  # 2등 점수
                rank.append("3등 공석")  # 3등 이름
                rank.append("0")  # 3등 점수
                print(rank)
            elif cnt == 2:
                rank.clear()
                rank.append(rs[0][0])  # 1등 이름
                rank.append(rs[0][1])  # 1등 점수
                rank.append(rs[1][0])  # 2등 이름
                rank.append(rs[1][1])  # 2등 점수
                rank.append("3등 공석")  # 3등 이름
                rank.append("0")  # 3등 점수
                print(rank)

            else:
                rank.clear()
                rank.append(rs[0][0])  # 1등 이름
                rank.append(rs[0][1])  # 1등 점수
                rank.append(rs[1][0])  # 2등 이름
                rank.append(rs[1][1])  # 2등 점수
                rank.append(rs[2][0])  # 3등 이름
                rank.append(rs[2][1])  # 3등 점수
                print(rank)
    finally:
        conn.close()


# 접속한 IP 주소 삽입
def connectInsert(ip):
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("insert into connect values ('" + ip + "');")  # IP 주소
        conn.commit()
    finally:
        conn.close()


# 접속했던 IP 주소 삭제
def connectDelete(ip):
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("delete from connect where ip = '" + ip + "';")
        conn.commit()
    finally:
        conn.close()