

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b8)
(ontable b3)
(on b4 b2)
(ontable b5)
(ontable b6)
(on b7 b9)
(on b8 b6)
(on b9 b1)
(clear b3)
(clear b5)
(clear b7)
)
(:goal
(and
(on b3 b1)
(on b4 b3)
(on b6 b8)
(on b7 b2)
(on b8 b7)
(on b9 b5))
)
)


