

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b9)
(on b3 b6)
(ontable b4)
(on b5 b4)
(on b6 b1)
(on b7 b3)
(on b8 b2)
(ontable b9)
(clear b5)
(clear b7)
)
(:goal
(and
(on b1 b8)
(on b3 b4)
(on b4 b7)
(on b5 b2)
(on b6 b9)
(on b7 b1)
(on b9 b5))
)
)


