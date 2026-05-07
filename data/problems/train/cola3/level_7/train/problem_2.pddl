

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b8)
(on b3 b2)
(on b4 b6)
(ontable b5)
(on b6 b9)
(ontable b7)
(on b8 b4)
(ontable b9)
(clear b1)
(clear b3)
(clear b5)
(clear b7)
)
(:goal
(and
(on b1 b7)
(on b2 b1)
(on b3 b6)
(on b5 b2)
(on b7 b9)
(on b8 b3))
)
)


