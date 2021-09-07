from functools import reduce


def convert_seconds(performance):
    if performance >= 60:
        minutes = performance / 60
        if minutes > 1:
            time = f"{round(minutes)} minute"
        else:
            time = f"{round(minutes)} minutes"
        if minutes >= 60:
            hours = minutes / 60
            if hours >= 60:
                time = f"{round(hours)} hour"
            else:
                time = f"{round(hours)} hours"
    else:
        time = performance
    return time


def convert_days(performance_days):
    if performance_days > 1:
        performance_days = f"{round(performance_days)} days"
    else:
        if performance_days is 1:
            performance_days = f"{round(performance_days)} day"
            control = True
        else:
            performance_days = f"{round(performance_days)} day"
            control = False
    context = {'performance': performance_days, 'control': control}
    return context


def percentage(mto_job, total_job):
    percentage_accept = (int(mto_job) / int(total_job)) * 100
    percentage_acceptance = round(percentage_accept)
    context = {'percentage_accept': percentage_accept, 'percentage_acceptance': percentage_acceptance}
    return context


def view_mto(request, id):
    mto = MTO.objects.get(pk=id)
    mto_job = MTOJob.objects.filter(assigned_to=id)

    days_list = [0]
    seconds_list = [0]
    for i in mto_job:
        if i.average_time is not 0:
            days_list.append(i.average_time.days)
            seconds_list.append(i.average_time.seconds)
    length = len(days_list) - 1
    # performance in days
    performance = reduce(lambda x, y: x + y, days_list)
    try:
        performance_days = round(performance / length)
    except ZeroDivisionError:
        performance_days = 0
    performance_days = convert_days(performance_days)

    # performance in seconds
    performance = reduce(lambda x, y: x + y, seconds_list)
    try:
        performance = performance / length
    except ZeroDivisionError:
        performance = 0
    performance = convert_seconds(performance)

    #  acceptance time calculating
    days = [0]
    seconds = [0]
    for i in mto_job:
        seconds.append(i.average_accept_time.seconds)
        days.append(i.average_accept_time.days)
    mto_job = MTOJob.objects.filter(assigned_to=id).count()
    accept_days = reduce(lambda x, y: x + y, days)
    try:
        accept_day = accept_days / mto_job
        accept_days = convert_days(accept_day)
    except ZeroDivisionError:
        accept_days = 0
    final_date = reduce(lambda x, y: x + y, seconds)
    try:
        accept_date = final_date / mto_job
        convert_seconds(accept_date)
    except ZeroDivisionError:
        time = 0
    mto_job = MTOJob.objects.filter(assigned_to=id).count()
    total_completed = MTOJob.objects.filter(
        completed_date__isnull=False, assigned_to=id).count()
    total_job = MTOJob.objects.all().count()
    try:
        percentage_acceptance = percentage(mto_job=mto_job, total_job=total_job)
    except ZeroDivisionError:
        percentage_acceptance = 0
    try:
        percentage_completeness = percentage(mto_job=mto_job, total_job=total_completed)
    except ZeroDivisionError:
        percentage_completeness = 0
    context = {'mto': mto, 'mto_job': mto_job, 'completed': total_completed,
               'per_completeness': percentage_completeness,
               'per_acceptance': percentage_acceptance, 'avg_accept_time': time,
               'avg_accept_days': accept_days,
               'performance_days': performance_days, 'performance': performance}
    return render(request, 'jobs/view_mto.html', context)
