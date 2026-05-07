

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b3)
(on b3 b1)
(ontable b4)
(on b5 b4)
(on b6 b8)
(on b7 b2)
(ontable b8)
(on b9 b5)
(clear b6)
(clear b7)
)
(:goal
(and
(on b4 b6)
(on b5 b8)
(on b6 b2)
(on b7 b9)
(on b8 b4))
)
)


