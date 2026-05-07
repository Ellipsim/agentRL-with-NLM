

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b10)
(on b4 b2)
(ontable b5)
(on b6 b5)
(on b7 b4)
(on b8 b9)
(on b9 b1)
(on b10 b6)
(clear b3)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b7)
(on b2 b3)
(on b5 b9)
(on b8 b1)
(on b10 b8))
)
)


