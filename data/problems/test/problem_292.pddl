

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b5)
(ontable b3)
(on b4 b7)
(on b5 b8)
(ontable b6)
(on b7 b2)
(ontable b8)
(clear b1)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b2)
(on b2 b5)
(on b3 b1)
(on b4 b6)
(on b5 b8)
(on b7 b3))
)
)


