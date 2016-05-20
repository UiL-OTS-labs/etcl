def copy_intervention_to_study(study, intervention):
    setting = intervention.setting.all()
    pre_r = intervention.pre_registrations.all()
    pre_rk = intervention.pre_registration_kinds.all()
    post_r = intervention.post_registrations.all()
    post_rk = intervention.post_registration_kinds.all()

    i = intervention
    i.pk = None
    i.study = study
    i.save()

    i.setting = setting
    i.pre_registrations = pre_r
    i.pre_registration_kinds = pre_rk
    i.post_registrations = post_r
    i.post_registration_kinds = post_rk
    i.save()
