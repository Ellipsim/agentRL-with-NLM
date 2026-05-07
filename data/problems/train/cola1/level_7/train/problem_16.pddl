

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b4)
(on b3 b2)
(on b4 b5)
(ontable b5)
(on b6 b9)
(ontable b7)
(on b8 b3)
(ontable b9)
(clear b1)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b7)
(on b3 b6)
(on b4 b3)
(on b6 b2)
(on b8 b1)
(on b9 b8))
)
)


