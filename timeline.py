class Timeline:
    def __init__(self, duration, function, **kwargs):
        self.playing = False
        self.finished = False
        self.starting_time = 0

        self.duration = duration
        self.kwargs = kwargs
        
        if self.duration == 0:
            def applied_func():
                function(0, self.kwargs)
            self.flags = [(0, applied_func)]
            self.function = Timeline.instant
        else:
            def applied_func():
                function(1, self.kwargs)
            self.flags = [(1, applied_func)]
            self.function = function
    
    def start(self, time):
        self.finished = False
        self.playing = True
        self.starting_time = time
        return self

    def play(self, current_time):
        if not self.playing:
            return
        if self.duration == 0:
            self.function(0, self.kwargs)
            return
        t = (current_time - self.starting_time)/self.duration
        while True:
            if len(self.flags) == 0:
                break
            (time, func) = self.flags[0]
            if t < time:
                break
            func()
            self.flags.pop(0)
        if t <= 1:
            self.function(t, self.kwargs)
        else:
            self.playing = False
            self.finished = True
    
    def par(animations):
        animation = animations[0]
        animations.pop(0)
        for anim in animations:
            animation = Timeline.par2(animation, anim)
        return animation

    def par2(a, b):
        if a.duration == 0:
            for flag in a.flags:
                b.flags.append(flag)
            b.sort_flags()
            return b
        if b.duration == 0:
            for flag in b.flags:
                a.flags.append(flag)
            a.sort_flags()
            return a
        new_dur = max(a.duration, b.duration)
        a_rat = a.duration / new_dur
        b_rat = b.duration / new_dur
        def new_func(t, _):
            if t <= a_rat:
                a.function(t / a_rat, a.kwargs)
            if t <= t * b.duration / new_dur:
                b.function(t / b_rat, b.kwargs)
        new_flags = []
        for flag in a.flags:
            (time, func) = flag
            time *= a.duration / new_dur
            new_flags.append((time, func))
        for flag in b.flags:
            (time, func) = flag
            time *= b.duration / new_dur
            new_flags.append((time, func))
        tl = Timeline(new_dur, new_func)
        tl.flags = new_flags
        tl.sort_flags()
        return tl
    
    def seq(animations):
        animation = animations[0]
        animations.pop(0)
        for anim in animations:
            animation = Timeline.seq2(animation, anim)
        return animation

    def seq2(a, b):
        if a.duration == 0:
            for flag in a.flags:
                b.flags.append(flag)
            b.sort_flags()
            return b
        new_dur = a.duration + b.duration
        a_rat = a.duration / new_dur
        if b.duration == 0:
            for flag in b.flags:
                (time, func) = flag
                a.flags.append((time + a_rat, func))
            a.sort_flags()
            return a
        b_rat = b.duration / new_dur
        def new_anim(t, _):
            if t <= a_rat:
                a.function(t / a_rat, a.kwargs)
            if t >= a_rat:
                b.function((t - a_rat) / b_rat, b.kwargs)
        new_flags = []
        for flag in a.flags:
            (time, func) = flag
            new_flags.append((time * a_rat, func))
        for flag in b.flags:
            (time, func) = flag
            new_flags.append((time * b_rat + a_rat, func))
        tl = Timeline(new_dur, new_anim)
        tl.flags = new_flags
        tl.sort_flags()
        return tl
    
    def sort_flags(self):
        self.flags.sort(key=lambda tup: tup[0])

    def is_finished(self, time):
        return self.finished

    def instant(_, kwargs):
        pass

    def wait(t):
        return Timeline(t, Timeline.instant)