

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(ontable b3)
(on b4 b8)
(on b5 b1)
(ontable b6)
(on b7 b3)
(on b8 b6)
(clear b4)
(clear b5)
(clear b7)
)
(:goal
(and
(on b2 b8)
(on b3 b1)
(on b6 b5)
(on b7 b6)
(on b8 b3))
)
)


