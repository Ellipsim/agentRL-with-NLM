

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b8)
(on b3 b6)
(on b4 b3)
(on b5 b7)
(ontable b6)
(ontable b7)
(ontable b8)
(clear b1)
(clear b2)
(clear b4)
)
(:goal
(and
(on b2 b6)
(on b3 b7)
(on b5 b2)
(on b7 b8)
(on b8 b1))
)
)


