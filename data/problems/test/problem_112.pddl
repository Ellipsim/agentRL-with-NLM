

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b7)
(ontable b2)
(ontable b3)
(on b4 b8)
(on b5 b1)
(ontable b6)
(on b7 b4)
(on b8 b3)
(clear b2)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b7)
(on b4 b1)
(on b5 b3)
(on b7 b5)
(on b8 b2))
)
)


