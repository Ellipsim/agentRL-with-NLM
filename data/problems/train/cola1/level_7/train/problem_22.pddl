

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b6)
(on b3 b1)
(on b4 b9)
(ontable b5)
(ontable b6)
(on b7 b3)
(on b8 b5)
(on b9 b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b4)
(on b2 b9)
(on b4 b8)
(on b7 b3)
(on b8 b6)
(on b9 b5))
)
)


