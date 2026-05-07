

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b5)
(on b3 b6)
(on b4 b7)
(ontable b5)
(ontable b6)
(on b7 b2)
(on b8 b9)
(on b9 b4)
(clear b1)
(clear b3)
)
(:goal
(and
(on b1 b8)
(on b3 b4)
(on b4 b9)
(on b5 b3)
(on b6 b1)
(on b9 b7))
)
)


