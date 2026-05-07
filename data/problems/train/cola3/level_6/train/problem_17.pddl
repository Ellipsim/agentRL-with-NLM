

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b1)
(on b3 b5)
(ontable b4)
(ontable b5)
(ontable b6)
(on b7 b2)
(ontable b8)
(clear b4)
(clear b6)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b8)
(on b2 b4)
(on b4 b7)
(on b6 b1)
(on b7 b6)
(on b8 b3))
)
)


