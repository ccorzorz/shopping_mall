#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz

import json,prettytable,time,collections
user_info=json.load(open('user_info','r'))
goods=json.load(open('goods_info','r'))
save_cart=json.load(open('save_cart','r'))
time_now=time.strftime('%Y-%m-%d %H:%M:%S')

def refresh_goods():
    json.dump(goods,open('goods_info','w'),ensure_ascii=False,indent=1)

def refresh_user():
    json.dump(user_info,open('user_info','w'),ensure_ascii=False,indent=1)

def cache_cart(user_name):
    save_cart[user_name]=cart
    # print('save_cart[user_name]',save_cart[user_name])
    json.dump(save_cart,open('save_cart','w'),ensure_ascii=False,indent=1)

def regis():
    exit_flag=0
    while exit_flag==0:
        user_name=input('请输入您的用户名:')
        if user_name in user_info.keys():
            print('此用户已被注册,请重新输入.')
        else:
            user_pwd=input('请输入您的密码:')
            for i in range(3):
                user_pwd_again=input('请再次确认您的密码:')
                if user_pwd_again==user_pwd:
                    user_info[user_name]=[user_pwd_again,0,[]]
                    refresh_user()
                    print('用户名%s已注册成功,请登录购买商品...'%user_name)
                    exit_flag=1
                    break
                elif i==2:
                    print('您输入的密码次数超过三次,注册关闭!')
                    exit_flag=1
                else:
                    print('您输入的密码和上次输入的密码不匹配,请重新输入,还有%s次机会.'%(2-i))
def refill(user_name):
    for i in range(3):
        amount=input('请输入您要充值的金额,请输入数字:')
        if amount.isdigit():
            user_info[user_name][1]+=int(amount)
            refresh_user()
            print('\033[32;1m土豪,请保养程序员!!!\033[0m充值成功,您的余额为\033[31;1m%s\033[0m'%user_info[user_name][1])
            balance=user_info[user_name][1]
            print(balance)
            break
        elif i==2:
            exit('你在坑我么?告诉你要输入数字的,程序关闭...')
        else:
            print('您输入的不是数字,请重新输入..')

def show_vcart(cart):
    # print(cart)
    if len(cart)>0:
        v_cart = collections.Counter(cart)
        dv_cart=dict(v_cart)
        row=prettytable.PrettyTable()
        row.field_names=['序列号','商品名称','商品数量','商品总价']
        for i in enumerate(dv_cart):
            index=i[0]
            item=i[1][0]
            totle_price = i[1][1] * dv_cart[i[1]]
            item_amount = dv_cart[i[1]]
            row.add_row([index,item,item_amount,totle_price])
        print(row)
    else:
        print('\033[31;1m购物车为空\033[0m'.center(50,'*'))
    time.sleep(1)

def check_cart():
    if len(cart)>0:
        v_cart=collections.Counter(cart)
        dv_cart=dict(v_cart)
        ddv_cart=[]
        for i in enumerate(dv_cart):
            index=i[0]
            item=i[1][0]
            totle_price = i[1][1] * dv_cart[i[1]]
            item_amount = dv_cart[i[1]]
            ddv_cart.append([item,item_amount,totle_price])
        user_info[user_name][2].append([time_now,ddv_cart])
        user_info[user_name][1]=balance
        refresh_user()
        refresh_goods()
        cart.clear()
        # print('cart:',cart)
        cache_cart(user_name)
        print('\033[31;1m结账成功,波多野结衣即将为您送货,请准备收货...\033[0m')
    else:
        print('\033[31;1m购物车是空的...\033[0m')
        cache_cart(user_name)
    time.sleep(1)

def show_his(user_name):
    user_info=json.load(open('user_info','r'))
    his_list=user_info[user_name][2]
    if len(his_list)==0:
        print('无购物历史...')
    else:
        for his in his_list:
            dt=his[0]
            print('\033[31;1m购物时间:%s\033[0m'.center(50,'*')%dt)
            row=prettytable.PrettyTable()
            row.field_names=['商品名称','数量','总额']
            for item in his[1]:
                p_name=item[0]
                p_amount=item[1]
                p_totle=item[2]
                row.add_row([p_name,p_amount,p_totle])
            print(row)

def edit_cart(user_name):
    e_cart=list(set(cart))
    e_vcart=collections.Counter(cart)
    e_vcart=dict(e_vcart)
    # print('e_vcart',e_vcart)
    e_cart.sort()
    # print('e_cart',e_cart)
    row=prettytable.PrettyTable()
    row.field_names=['商品序列号','商品名称','商品数量','总价']
    for i in enumerate(e_cart):
        index=i[0]
        p_name=i[1][0]
        p_price=i[1][1]
        p_amount=e_vcart[i[1]]
        p_totle=i[1][1]*e_vcart[i[1]]
        p_belong=i[1][2]
        # print(index,p_name,p_price,p_amount,p_totle,p_belong)
        row.add_row([index,p_name,p_amount,p_totle])
    print(row)
    while True:
        choice_num=input('请输入要编辑的商品序列号,输入q或quit为退出编辑购物车:')
        if choice_num.isdigit() and  int(choice_num)<len(e_cart):
            choice_num=int(choice_num)
            goods_stock=goods[e_cart[choice_num][2]][e_cart[choice_num][0]]['stock']
            p_amount=e_vcart[e_cart[choice_num]]
            balance=user_info[user_name][1]
            print(goods_stock)
            while True:
                choice_num_d=input('输入要购买的商品数量:')
                if choice_num_d.isdigit():
                    choice_num_d=int(choice_num_d)
                    if choice_num_d<=goods_stock:
                        if choice_num_d==p_amount:
                            print('修改商品数量成功')
                            break
                        elif choice_num_d>p_amount:
                            d_price=int(choice_num_d-p_amount)*int(e_vcart[e_cart[choice_num]])
                            if balance>=d_price:
                                for i in range(choice_num_d-p_amount):
                                    cart.append(e_cart[choice_num])
                                balance-=d_price
                                goods_stock+=p_amount
                                goods_stock-=choice_num_d
                            else:
                                print('余额不足,修改失败,请充值!')
                                break
                        else:
                            d_price=int(abs(choice_num_d-p_amount))*(e_vcart[e_cart[choice_num]])
                            for i in range(abs(choice_num_d-p_amount)):
                                cart.remove(e_cart[choice_num])
                            balance+=d_price
                            goods_stock+=p_amount
                            goods_stock-=choice_num_d
                            print('修改成功.')
                            break
                    else:
                        print('输入数量有误,请合适商品的库存...')
                        break
                else:
                    print('输入类型有误请重新输入...')
                    break
        elif choice_num == 'q' or choice_num == 'quit':
            print('退出编辑购物车...')
            break
        else:
            print('输入有误,请重新输入...')


break_flag=0
user_lock=open('user_lock','r+')
locker=user_lock.readlines()

user_name=input('请输入\033[31;1m壕\033[0m的用户名:')
if  user_name in locker:
    exit('用户已被锁定')
if user_name in json.load(open('user_info','r')).keys() and user_info not in locker:
    for i in range(3):
        if break_flag==1:
            break
        else:
            pwd=input('请输入%s的密码:'%user_name)
            if pwd==user_info[user_name][0]:
                if save_cart.get(user_name)==None:
                    cart=[]
                else:
                    cart=save_cart[user_name]
                    for i in range(len(cart)):
                        cart[i]=tuple(cart[i])
                    # print('转换后cart:',cart)
                print('登陆成功...')
                print('欢迎来到大牛逼商城,走过路过,不要错过...'.center(50,'*'))
                while break_flag==0:
                    if save_cart.get(user_name)==None or len(save_cart[user_name])<=0:
                        balance = user_info[user_name][1]
                        print('壕,您的账户余额为:\033[31;1m%s\033[0m,\033[32;1m(钱不够?账户充值请输入r,回车继续购物)\033[0m:'%balance)
                    else:
                        cart_price_list=[]
                        for i in cart:
                            cart_price_list.append(i[1])
                        balance=user_info[user_name][1]-sum(cart_price_list)
                        print('\033[31;1m您的购物车中还有您上次购物时未结算的商品,如减去购物车中的商品总价,您的余额为\033[0m\033[31;1m%s\033[0m'%balance)
                        time.sleep(1)
                    mrow=prettytable.PrettyTable()
                    mrow.field_names=['功能','购物','查看购物车','查看购物历史','余额充值','退出购物商城','确认购买','编辑购物车']
                    mrow.add_row(['快捷键','回车','S或showcart','H或history','R或refill','Q或quit','C或check','E或者edit'])
                    print(mrow)
                    menu=input('''\033[32;1m选择菜单:\033[0m''')
                    if menu.lower()=='r':
                        refill(user_name)
                    elif menu.lower()=='h' or menu.lower()=='history':
                        time.sleep(1)
                        show_his(user_name)
                        time.sleep(1)
                    elif menu.lower()=='s' or menu.lower()=='showcart' :
                        time.sleep(1)
                        show_vcart(cart)
                    elif menu.lower()=='c' or menu.lower()=='check':
                        check_cart()
                    elif menu.lower()=='q' or menu.lower()=='quit':
                        break_flag=1
                        cache_cart(user_name)
                    elif menu.lower()=='e' or menu.lower()=='edit':
                        edit_cart(user_name)
                    elif len(menu)==0:
                        while break_flag==0:
                            print('壕,您的扣除购物车中的钱款预计账户余额为:\033[31;1m%s\033[0m:'%balance)
                            print('请选择商品的类型编号'.center(50,'='))
                                # print(list(goods.keys()))
                            cla_list=list(goods.keys())
                            for i in cla_list:
                                print(cla_list.index(i),i)
                            choice_cla_num=input('''\033[32;1m请选择您要购买物品类型所对应的序列号(返回主菜单输入'b'或'back',查看购物车输入s,确认付款输入c,退出输入q或quit):\033[0m''')
                            if choice_cla_num.isdigit() and int(choice_cla_num)<len(cla_list):
                                choice_cla_num=int(choice_cla_num)
                                cla=cla_list[choice_cla_num]
                                goods_list=list(goods[cla])
                                while break_flag==0:
                                    if len(cart)==0:
                                        print('壕,您的目前账户余额为:\033[31;1m%s\033[0m'%balance)
                                    else:
                                        print('壕,您购买购物车中商品后,预计账户余额为:\033[31;1m%s\033[0m'%balance)
                                    row=prettytable.PrettyTable()
                                    row.field_names=['序列号','商品名称','商品价格','商品库存']
                                    for p in goods_list:
                                        p_num=goods_list.index(p)
                                        p_name=p
                                        p_price=goods[cla][p]['price']
                                        p_stock=goods[cla][p]['stock']
                                        row.add_row([p_num,p_name,p_price,p_stock])
                                    print(row)
                                    choice_p_num=input('\033[32;1m输入您要购买的商品序列号,返回商品分类请输入b或back,查看购物车输入s,确认付款输入c,退出系统输入q或quit:\033[0m')
                                    if choice_p_num.isdigit() and int(choice_p_num)<len(goods_list):
                                        p_name=goods_list[int(choice_p_num)]
                                        p_price=goods[cla][p_name]['price']
                                        p_stock=goods[cla][p_name]['stock']
                                        p_belong=goods[cla][p_name]['belong']
                                        while break_flag==0:
                                            p_count=input('\033[32;1m输入您要购买的商品数量,直接回车系统默认数量默1:\033[0m')
                                            if len(p_count)==0:
                                                p_count=1
                                            elif p_count.isdigit():
                                                if int(p_count) <= p_stock:
                                                    p_count = int(p_count)
                                                else:
                                                    print('库存数量有限,最大购买数量为%s' % p_stock)
                                                    break

                                            if balance >= p_count*p_price:
                                                p_stock-=p_count
                                                goods[cla][p_name]['stock']=p_stock
                                                for i in range(p_count):
                                                    cart.append((p_name,p_price,p_belong))
                                                # print(cart)
                                                print('商品\033[32;1m%s\033[0m已加入购物车'%p_name)
                                                v_cart=collections.Counter(cart)
                                                print('\033[31;1m未付款商品\033[0m'.center(50,'*'))
                                                show_vcart(v_cart)
                                                balance-=p_count*p_price
                                                break
                                            else:
                                                print('您的预计余额已不足购买\033[31;1m%s件%s\033[0m，请重新确认商品价格以及数量,也可返回主菜单编辑购物车.'%(p_count,p_name))
                                                print('\033[31;1m您可返回主菜单进入充值系统充值,8亿10亿不是事儿...\033[0m')
                                                time.sleep(1)
                                                break

                                    elif choice_p_num.lower()=='b' or choice_p_num.lower=='back':
                                        break
                                    elif choice_p_num.lower()=='s':
                                        show_vcart(cart)
                                    elif choice_p_num.lower()=='c' or choice_p_num.lower()=='check':
                                        check_cart()
                                    elif choice_p_num.lower()=='q' or choice_p_num.lower()=='quit':
                                        break_flag=1
                                        cache_cart(user_name)
                                    else:
                                        print('输入类型错误,请重新输入')
                                        time.sleep(1)
                            elif choice_cla_num.lower()=='s'or choice_cla_num.lower()=='showcart':
                                show_vcart(cart)
                            elif choice_cla_num.lower()=='c' or choice_cla_num.lower()=='check':
                                check_cart()
                            elif choice_cla_num.lower()=='b'or choice_cla_num.lower()=='back':
                                break
                            elif choice_cla_num.lower()=='q' or choice_cla_num.lower()=='quit':
                                break_flag=1
                                cache_cart(user_name)
                            elif choice_cla_num.lower()=='e' or choice_cla_num.lower()=='edit':
                                edit_cart(user_name)
                            else:
                                print('输入有误,请重新输入')
            elif i==2:
                user_lock.write('\n%s'%user_name)
                user_lock.close()
                exit('三次密码错误,账户已被锁定')
            else:
                print('密码错误,请重新输入...')
else:
    y_or_n=input('没有此用户名,需要注册才能进入商城!!!是否要注册?\033[31;1m输入y或者回车为注册,n或者q退出\033[0m:')
    if len(y_or_n)==0 or y_or_n=='y':
        regis()
    elif y_or_n=='n' or y_or_n=='q':
        exit('程序退出...')
    else:
        exit('输入错误,程序退出...')

