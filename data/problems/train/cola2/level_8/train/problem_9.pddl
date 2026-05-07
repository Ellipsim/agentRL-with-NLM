

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(on b3 b1)
(on b4 b3)
(ontable b5)
(on b6 b2)
(ontable b7)
(ontable b8)
(on b9 b8)
(clear b4)
(clear b6)
(clear b7)
(clear b9)
)
(:goal
(and
(on b1 b7)
(on b2 b6)
(on b3 b9)
(on b5 b8)
(on b6 b1)
(on b8 b3))
)
)


