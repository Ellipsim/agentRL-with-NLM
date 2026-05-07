

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b1)
(ontable b4)
(on b5 b6)
(on b6 b9)
(ontable b7)
(ontable b8)
(on b9 b4)
(clear b2)
(clear b3)
(clear b5)
(clear b7)
(clear b8)
)
(:goal
(and
(on b3 b7)
(on b4 b9)
(on b5 b4)
(on b6 b8)
(on b7 b6)
(on b9 b2))
)
)


