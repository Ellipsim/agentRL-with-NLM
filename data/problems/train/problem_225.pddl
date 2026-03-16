

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(ontable b3)
(on b4 b8)
(on b5 b4)
(on b6 b2)
(ontable b7)
(on b8 b9)
(ontable b9)
(clear b1)
(clear b3)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b2)
(on b3 b5)
(on b4 b1)
(on b6 b9)
(on b7 b4)
(on b9 b3))
)
)


