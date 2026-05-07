

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b1)
(on b3 b7)
(ontable b4)
(ontable b5)
(on b6 b8)
(ontable b7)
(on b8 b4)
(clear b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b1 b4)
(on b2 b6)
(on b5 b3)
(on b6 b1)
(on b7 b2))
)
)


