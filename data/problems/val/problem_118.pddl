

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b9)
(ontable b3)
(on b4 b6)
(ontable b5)
(on b6 b2)
(on b7 b1)
(on b8 b5)
(on b9 b10)
(ontable b10)
(clear b3)
(clear b7)
(clear b8)
)
(:goal
(and
(on b2 b4)
(on b3 b6)
(on b5 b8)
(on b7 b9)
(on b8 b10)
(on b10 b7))
)
)


