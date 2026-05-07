

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b5)
(on b3 b9)
(on b4 b6)
(ontable b5)
(on b6 b2)
(ontable b7)
(on b8 b3)
(ontable b9)
(clear b1)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b2)
(on b4 b9)
(on b6 b7)
(on b7 b5)
(on b8 b6)
(on b9 b3))
)
)


