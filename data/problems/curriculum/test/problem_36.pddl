

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b7)
(on b3 b2)
(ontable b4)
(on b5 b1)
(on b6 b4)
(on b7 b8)
(ontable b8)
(on b9 b3)
(clear b5)
(clear b9)
)
(:goal
(and
(on b3 b8)
(on b4 b3)
(on b5 b4)
(on b6 b5)
(on b9 b7))
)
)


