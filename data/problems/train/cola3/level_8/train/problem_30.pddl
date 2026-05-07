

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b5)
(ontable b3)
(on b4 b6)
(on b5 b7)
(on b6 b8)
(on b7 b3)
(ontable b8)
(ontable b9)
(clear b1)
(clear b2)
(clear b9)
)
(:goal
(and
(on b2 b9)
(on b4 b8)
(on b5 b2)
(on b6 b5)
(on b7 b4)
(on b8 b3))
)
)


