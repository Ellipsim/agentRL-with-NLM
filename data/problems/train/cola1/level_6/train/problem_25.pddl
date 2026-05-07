

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b1)
(on b3 b7)
(ontable b4)
(on b5 b8)
(on b6 b4)
(ontable b7)
(ontable b8)
(clear b2)
(clear b3)
(clear b6)
)
(:goal
(and
(on b2 b7)
(on b3 b2)
(on b4 b1)
(on b5 b6)
(on b6 b4)
(on b8 b3))
)
)


