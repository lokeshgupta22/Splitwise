import os


def display(db):
    print(db)


def split_equally(amt, db, mp, total, divsplit):
    topay = amt/(len(divsplit))
    topay = round(topay, 2)
    for n in divsplit:
        if n == mp:
            if db[mp] == 0:
                db[mp] = f"You get {topay * (len(divsplit) - 1)}"
            else:
                db[mp] += f"{chr(10)}You get {topay * (len(divsplit) - 1)}"
            total[mp] += topay * (len(divsplit) - 1)
        else:
            if db[n] == 0:
                db[n] = f"Pay {-1 * topay} to {mp}"
            else:
                db[n] += f"{os.linesep}Pay {-1 * topay} to {mp}"
            total[n] += -1 * topay
    return db


def split_unequally(amt, db, mp, total, divsplit):
    for i in divsplit:
        part = int(input(f"Enter amount spent on {i}: "))
        if i == mp:
            if db[mp] == 0:
                db[mp] = f"You get {(amt - part)}"
            else:
                db[mp] += f"{chr(10)}You get {(amt - part)}"
            total[mp] += (amt - part)
        else:
            if db[i] == 0:
                db[i] = f"Pay {-1 * part} to {mp}"
            else:
                db[i] += f"{os.linesep}Pay {-1 * part} to {mp}"
            total[i] += (-1*part)
    return db


def single_payer(amt, db, mp, total):
    div = input("Enter names of members to split: ")
    divsplit = div.split(' ')
    eq = input("Do you want to split equally? (y/n): ")
    if eq == "y":
        db = split_equally(amt, db, mp, total, divsplit)
        display(db)
    elif eq == "n":
        db = split_unequally(amt, db, mp, total, divsplit)
        display(db)
    else:
        print("Invalid")
        print("Try Again!")
        single_payer(amt, db, mp, total)


def split_equally_mp(totalamt, db, mps, multi, total, divsplit):
    topay = totalamt/(len(divsplit))
    topay = round(topay, 2)
    payee = mps
    for n in divsplit:
        if n in mps:
            pos = mps.index(n)
            amtofn = multi[pos]
            fin = amtofn - topay
            if fin > 0:
                if db[n] == 0:
                    db[n] = f"You get {fin}"
                else:
                    db[n] += f"{chr(10)}You get {fin}"
                total[n] += (amtofn - topay)
            else:
                payee.remove(n)
                if db[n] == 0:
                    db[n] = f"Pay {fin} to {payee}"
                else:
                    db[n] += f"{os.linesep}Pay {fin} to {payee}"
                total[n] += (amtofn - topay)

        else:
            if db[n] == 0:
                db[n] = f"Pay {-1 * topay} to {payee}"
            else:
                db[n] += f"{os.linesep}Pay {-1 * topay} to {payee}"
            total[n] += -1 * topay
    return db


def split_unequally_mp(totalamt, db, mps, multi, total, divsplit):
    print("Feature is still under development!")
    return db


def multiple_payer(db, mps, total):
    multi = []
    totalamt = 0
    for p in mps:
        amtperperson = int(input(f"Enter amount paid by {p}: "))
        multi.append(amtperperson)
        totalamt += amtperperson

    div = input("Enter names of members to split: ")
    divsplit = div.split(' ')
    eq = input("Do you want to split equally? (y/n): ")
    if eq == "y":
        db = split_equally_mp(totalamt, db, mps, multi, total, divsplit)
        display(db)
    elif eq == "n":
        db = split_unequally_mp(totalamt, db, mps, multi, total, divsplit)
        display(db)
    else:
        print("Invalid")
        print("Try Again!")
        multiple_payer(db, mps, total)


def expense(amt, db, total):
    mp = input("Enter names of members who paid: ")
    mps = mp.split(' ')
    if len(mps) == 1:
        single_payer(amt, db, mp, total)
        return total
    else:
        multiple_payer(db, mps, total)
        return total


def settle_up(db, total):
    e = 0
    for t in total:
        if total[t] > 0:
            e += 1
    if e == 0:
        print("All the people in the group are settled up.")
        continued(db, total)
    a = input("Enter your name (name of payer): ")
    b = input("Enter name of who you want to settle up payment: ")
    settleamt = min(abs(total[a]), abs(total[b]))
    ch = input(
        f"You need to pay {settleamt}. Do you want to settle up?(y/n): ")
    if ch == "y":
        total[a] += settleamt
        total[b] -= settleamt
        if total[a] == 0:
            db[a] = f"You are settled up."
            if total[b] > 0:
                db[b] = f"You get {total[b]}"
            elif total[b] < 0:
                db[b] = f"Pay {total[b]}"
            else:
                db[b] = f"You are settled up."
        elif total[b] == 0:
            db[b] = f"You are settled up."
            if total[a] > 0:
                db[a] = f"You get {total[a]}"
            elif total[a] < 0:
                db[a] = f"Pay {total[a]}"
            else:
                db[a] = f"You are settled up."
    else:
        print("Payment cancelled.")
    return db


def continued(db, total):
    re = input("Would you like to use the app again? (y/n): ")
    if re == "total":
        k = 2
        res = {}
        for key in total:
            res[key] = round(total[key], k)
        print(res)
        continued(db, total)
    elif re == "db":
        print(db)
        continued(db, total)
    elif re == "y":
        operate(db, total)
    elif re == "n":
        exit(0)
    else:
        print("Invalid")
        exit(0)


def operate(db, total):
    op = int(input("Enter Operation (1-Enter Expense/2-Settle Up): "))
    if op == 1:
        a = int(input("Enter Expense: "))
        expense(a, db, total)
        continued(db, total)
    elif op == 2:
        settle_up(db, total)
        continued(db, total)
    elif op == 99:
        exit(0)
    else:
        print("Invalid")
        exit(0)


def createdb():
    mem = int(input("Enter No. of members in group: "))
    n = mem
    db = {}
    total = {}
    while n > 0:
        nme = input(f"Enter Name of Member {mem - n +1}: ")
        if nme in db or nme == " ":
            print("Please use a Unique Name.")
            n += 1
        db.update({nme: 0})
        total.update({nme: 0})
        n -= 1
    # db = {'r': 0, 'l': 0, 'd': 0}
    # total = {'r': 0, 'l': 0, 'd': 0}
    operate(db, total)


createdb()
