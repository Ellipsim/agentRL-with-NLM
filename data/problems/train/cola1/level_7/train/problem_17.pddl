

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b6)
(on b3 b9)
(on b4 b2)
(ontable b5)
(on b6 b3)
(on b7 b5)
(ontable b8)
(ontable b9)
(clear b1)
(clear b7)
(clear b8)
)
(:goal
(and
(on b2 b1)
(on b3 b8)
(on b4 b5)
(on b7 b2)
(on b9 b3))
)
)


