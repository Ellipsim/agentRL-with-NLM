

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b9)
(on b3 b5)
(on b4 b11)
(ontable b5)
(on b6 b4)
(ontable b7)
(on b8 b6)
(on b9 b8)
(ontable b10)
(on b11 b7)
(on b12 b1)
(clear b2)
(clear b10)
(clear b12)
)
(:goal
(and
(on b2 b5)
(on b3 b4)
(on b4 b1)
(on b5 b3)
(on b7 b9)
(on b8 b2)
(on b9 b12)
(on b10 b11)
(on b11 b6))
)
)


