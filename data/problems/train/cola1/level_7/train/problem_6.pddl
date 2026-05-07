

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b7)
(on b3 b6)
(on b4 b5)
(ontable b5)
(on b6 b8)
(on b7 b4)
(on b8 b2)
(on b9 b3)
(clear b1)
)
(:goal
(and
(on b2 b3)
(on b4 b9)
(on b6 b2)
(on b8 b1)
(on b9 b5))
)
)


